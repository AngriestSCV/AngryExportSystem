#if UNITY_EDITOR

using UnityEngine;

namespace AngryLabs.AngryExportSystem
{
    public interface IFbxImportPass
    {
        bool ImportPass(ProcessFbxImport importer, GameObject go, AngryExportSystemXml options);
    }
}
#endif