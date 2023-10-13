#if UNITY_EDITOR

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml.Serialization;
using UnityEditor;
using UnityEditor.AssetImporters;
using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    public class ProcessFbxImport : AssetPostprocessor
    {
        private readonly Dictionary<string, AngryExportSystemXml> _userPropertyMap = new Dictionary<string, AngryExportSystemXml>();

        static XmlSerializer _exportSeralizer = new XmlSerializer(typeof(AngryExportSystemXml));

        private void OnPostprocessGameObjectWithUserProperties(GameObject go, string[] propNames, object[] values)
        {
            AngryExportSystemXml options = null;
            for (int i = 0; i < propNames.Length; i++)
            {
                if (propNames[i] == "AngryExportSystem_Xml")
                {
                    try
                    {
                        var ms = new MemoryStream();
                        var xml_string = values[i] as string;
                        var asBytes = Encoding.UTF8.GetBytes(xml_string);
                        ms.Write(asBytes, 0, asBytes.Length);
                        ms.Position = 0;
                        options = _exportSeralizer.Deserialize(ms) as AngryExportSystemXml;
                    }
                    catch (Exception ex)
                    {
                        Debug.LogError($"Error deseralizing AngryExportSystemXml on [{go.name}] [{ex}]");
                        options = null;
                    }
                }
            }

            if (options != null)
            {
                _userPropertyMap.Add(go.name, options);
            }
        }

        public bool SkipAsset(string path)
        {
            path = path.Replace("\\", "/");
            bool process =  path.ToLower().Contains("assets/automeshes") || path.ToLower().Contains("assets/props");
            return !process;
        }

        public void OnPreprocessModel()
        {
            if (SkipAsset(assetPath)) return;
            ModelImporter modelImporter = assetImporter as ModelImporter;
            if (modelImporter == null) return;

            modelImporter.materialImportMode = ModelImporterMaterialImportMode.ImportStandard;

            modelImporter.isReadable = true;
            modelImporter.generateSecondaryUV = !assetPath.Contains(".uved");
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
                AngryExportSystemXml options;
                _userPropertyMap.TryGetValue(target.name, out options);

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

            if (SkipAsset(assetPath)) return;

            HandleStaticFlags(model, default(StaticEditorFlags));
            var passes = new IFbxImportPass[]
            {
                new PrefabReplacementPass(),
                new ProcessLightmapScale(),
                new CollisionPass(),
                new RenderPass(),
                new ChangeMaterialPass(this),
            };

            RecursiveVisit(model, passes);
        }

        private void HandleStaticFlags(GameObject obj, StaticEditorFlags initial_flags)
        {
            if (_userPropertyMap.TryGetValue(obj.name, out AngryExportSystemXml options) &&
                options?.StaticFlags?.Flags != null)
            {
                initial_flags = default(StaticEditorFlags);
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