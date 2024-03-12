#if UNITY_EDITOR

using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    class ProcessLightmapScale : IFbxImportPass
    {
        public bool ImportPass(ProcessFbxImport importer, GameObject go, ExportObject options)
        {
            var light = options?.LightmapScale;
            if (light == null) return true;

            if(!go.TryGetComponent<MeshRenderer>(out var mr))
            {
                Debug.LogError($"Can not apply light map scale to items without a {nameof(MeshRenderer)}");
                return true;
            }

            mr.scaleInLightmap = options.LightmapScale.Scale;
            return true;
        }
    }
}
#endif