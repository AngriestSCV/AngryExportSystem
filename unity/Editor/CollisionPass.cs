#if UNITY_EDITOR

using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    class CollisionPass : IFbxImportPass
    {
        public bool ImportPass(ProcessFbxImport importer, GameObject go, AngryExportSystemXml options)
        {
            var colType = options?.Collider;
            if (colType == null) return true;


            switch (colType.ColliderType)
            {
                case "Mesh":
                    {
                        var mc = (MeshCollider)go.AddComponent(typeof(MeshCollider));
                        mc.enabled = true;
                        mc.convex = false;
                    }
                    break;
                case "Box":
                    {
                        var bx = (BoxCollider)go.AddComponent(typeof(BoxCollider));
                        bx.enabled = true;
                    }
                    break;
                default:
                    Debug.LogError($"Unknown collision type on [{go.name}]: [{colType.ColliderType}]");
                    break;
            }
            return true;
        }
    }

}
#endif