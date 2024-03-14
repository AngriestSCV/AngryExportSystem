#if UNITY_EDITOR

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Xml.Serialization;
using UnityEditor;
using UnityEditor.AssetImporters;
using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    public class ProcessFbxImport : AssetPostprocessor
    {
        static XmlSerializer _exportSeralizer = new XmlSerializer(typeof(AngryExportSystemList));
        private AngryExportSystemList _importConfig;

        private void OnPostprocessGameObjectWithUserProperties(GameObject go, string[] propNames, object[] values)
        {
        }

        private bool TryLoadXml(string assetPath, out AngryExportSystemList cfg)
        {
            try
            {
                if (!File.Exists(assetPath))
                {
                    cfg = null;
                    return false;
                }

                using (var xmlFile = File.OpenRead(assetPath))
                {
                    cfg = _exportSeralizer.Deserialize(xmlFile) as AngryExportSystemList;
                }
                return true;
            }
            catch(Exception ex)
            {
                Debug.LogError($"Exception while trying to load XML file: {assetPath}");
                Debug.LogException(ex);

                cfg = null;
                return false;
            }
        }


        public void OnPreprocessModel()
        {
            if (!TryLoadXml(assetImporter.assetPath + ".xml", out var cfg))
                return;

            _importConfig = cfg;


            ModelImporter modelImporter = assetImporter as ModelImporter;
            if (modelImporter == null) return;

            modelImporter.materialImportMode = ModelImporterMaterialImportMode.ImportStandard;

            modelImporter.isReadable = true;
            modelImporter.generateSecondaryUV = _importConfig?.GenerateLightmap?.Value ?? false;
            modelImporter.preserveHierarchy = true;
        }

        void RecursiveVisit(GameObject target, IFbxImportPass[] passes)
        {
            var children = new List<GameObject>(target.transform.childCount);
            for (int i = 0; i < target.transform.childCount; i++)
            {
                var c = target.transform.GetChild(i);
                children.Add(c.gameObject);
            }

            foreach(var pass in passes)
            { 
                ExportObject options;
                _importConfig.Lookup.TryGetValue(target.name, out options);

                if(!pass.ImportPass(this, target, options))
                {
                    return;
                }
            }

            foreach(var child in children)
            {
                RecursiveVisit(child, passes);
            }
        }


        private void OnPostprocessModel(GameObject model)
        {
            if (_importConfig == null)
                return;

            HandleStaticFlags(model, default);
            var passes = new IFbxImportPass[]
            {
                new PrefabReplacementPass(),
                new ProcessLightmapScale(),
                new CollisionPass(),
                new RenderPass(),
                new ChangeMaterialPass(this),
                new ExportPass(),
            };

            RecursiveVisit(model, passes);
        }

        private void HandleStaticFlags(GameObject obj, StaticEditorFlags initial_flags)
        {
            if (_importConfig.Lookup.TryGetValue(obj.name, out ExportObject options) &&
                options?.StaticFlags?.Flags != null)
            {
                initial_flags = default;
                foreach (var flagString in options.StaticFlags.Flags)
                {
                    if (Enum.TryParse(flagString, out StaticEditorFlags flag))
                    {
                        initial_flags |= flag;
                    }
                    else
                    {
                        Debug.LogWarning($"Could not convert [{flagString}] to a StaticEditorFlag on [{obj.name}]");
                    }
                }
            }

            GameObjectUtility.SetStaticEditorFlags(obj, initial_flags);

            int child_count = obj.transform.childCount;
            for (int i = 0; i < child_count; i++)
            {
                var next = obj.transform.GetChild(i).gameObject;
                HandleStaticFlags(next, initial_flags);
            }
        }
    }

}
#endif