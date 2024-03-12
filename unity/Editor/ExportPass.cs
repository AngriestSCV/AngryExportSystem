using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    internal class ExportPass : IFbxImportPass
    {
        public bool ImportPass(ProcessFbxImport importer, GameObject go, ExportObject options)
        {
            bool export = options?.Export?.Enabled ?? true;
            if (!export)
                UnityEngine.Object.DestroyImmediate(go, true);
            return export;
        }
    }
}