#if UNITY_EDITOR

using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    public class ChangeMaterialPass : IFbxImportPass
    {
        public ChangeMaterialPass(ProcessFbxImport  importer)
        {
            string path = Path.GetDirectoryName(importer.assetPath);
            MaterialDic = FindValidMaterials(path);
        }

        private Dictionary<string, string> FindValidMaterials(string startPath)
        {
            Dictionary<string, string> ret = new Dictionary<string, string>();

            var pathsToSearch = new List<string>();

            string[] parts = startPath.Split('\\', '/');

            string curPath = parts[0];
            pathsToSearch.Add($"{curPath}/materials");

            for (int i = 1; i < parts.Length; i++)
            {
                curPath = $"{curPath}/{parts[i]}";
                pathsToSearch.Add($"{curPath}/materials");
            }
            pathsToSearch.Reverse();

            foreach (var path in pathsToSearch)
            {
                var guids = AssetDatabase.FindAssets("t:material", new string[] { path });

                var testPaths = guids.Select(AssetDatabase.GUIDToAssetPath);

                foreach (var testPath in testPaths)
                {
                    var baseName = Path.GetFileNameWithoutExtension(testPath);
                    if (ret.ContainsKey(baseName)) continue;

                    ret.Add(baseName, testPath);
                }
            }
            return ret;
        }
        public Dictionary<string, string> MaterialDic { get; private set; }


        public bool ImportPass(ProcessFbxImport importer, GameObject target, ExportObject options)
        {
            Renderer rend;
            if (!target.TryGetComponent<Renderer>(out rend))
            {
                return true;
            }

            var materials = rend.sharedMaterials;

            if (materials == null)
            {
                Debug.LogError($"Error could not find shared materials on object [{target.name}]");
                return true;
            }

            var newMats = new Material[materials.Length];

            for (int i = 0; i < materials.Length; i++)
            {
                Material mat = materials[i];
                newMats[i] = mat;

                if (mat == null)
                {
                    Debug.LogError($"Found null material at index [{i}] on [{target.name}]");
                    continue;
                }

                Material newMat;
                string matPath = "";
                if (MaterialDic.TryGetValue(mat.name, out matPath))
                {
                    newMat = AssetDatabase.LoadAssetAtPath<Material>(matPath);
                    if (newMat == null)
                    {
                        Debug.LogError($"Failed to load material at path [{matPath}]");
                        continue;
                    }

                }
                else
                {
                    Debug.LogWarning($"Could not find material replacment for material [{mat.name}] on object [{target.name}]");
                    var shader = Shader.Find("Standard");
                    newMat = new Material(shader);
                    string dir = Path.GetDirectoryName(importer.assetPath);
                    dir = Path.Combine(dir, "materials");
                    if (!Directory.Exists(dir))
                    {
                        Directory.CreateDirectory(dir);
                    }
                    string matFileName = mat.name + ".asset";
                    string matName = Path.Combine(dir, matFileName);
                    AssetDatabase.CreateAsset(newMat, matName);

                    MaterialDic[mat.name] = matName;
                }
                newMats[i] = newMat;

            }
            rend.sharedMaterials = newMats;
            return true;
        }
    }
}
#endif