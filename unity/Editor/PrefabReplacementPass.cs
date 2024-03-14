#if UNITY_EDITOR

using System.IO;
using UnityEditor;
using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    class PrefabReplacementPass : IFbxImportPass
    {
        public bool ImportPass(ProcessFbxImport importer, GameObject go, ExportObject options)
        {
            var pre = options?.PrefabLink;
            if (pre == null) return true;

            string value = pre.PrefabPath;
            if (!File.Exists(pre.PrefabPath))
            {
                Debug.LogError($"Failed to find the prefab at [{value}] for [{go.name}]");
                return true;
            }


            var obj = AssetDatabase.LoadAssetAtPath<GameObject>(value);
            if (obj == null)
            {
                Debug.LogError($"Prefab [{value}] failed to load");
                return true;
            }

            obj = PrefabUtility.InstantiatePrefab(obj) as GameObject;
            var par = go.transform.parent;
            obj.transform.SetPositionAndRotation(go.transform.position, go.transform.rotation);
            //obj.transform.localScale = go.transform.localScale;
            obj.transform.Rotate(Vector3.right, 90.0f);
            go.SetActive(false);

            obj.name = go.name + ".prefab";
            UnityEngine.Object.DestroyImmediate(go, true);
            obj.transform.parent = par;

            return false;
        }
    }

}
#endif