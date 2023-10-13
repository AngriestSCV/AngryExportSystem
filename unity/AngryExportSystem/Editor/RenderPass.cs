#if UNITY_EDITOR

using UnityEngine;
using static AngryLabs.AngryExportSystem.ProcessFbxImport;

namespace AngryLabs.AngryExportSystem
{
    class RenderPass : IFbxImportPass
    {
        public bool ImportPass(ProcessFbxImport importer, GameObject go, AngryExportSystemXml options)
        {
            var value = options?.Render;
            if (value == null) return true;

            if (value.Enabled) return true;

            if (go.TryGetComponent(out MeshRenderer mr))
            {
                UnityEngine.Object.DestroyImmediate(mr, true);
            }
            if (go.TryGetComponent(out SkinnedMeshRenderer smr))
            {
                UnityEngine.Object.DestroyImmediate(smr, true);
            }

            return true;
        }
    }
}
#endif