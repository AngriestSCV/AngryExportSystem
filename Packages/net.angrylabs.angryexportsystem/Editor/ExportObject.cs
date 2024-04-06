using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Xml.Serialization;
using UnityEditor;

namespace AngryLabs.AngryExportSystem
{
    [XmlRoot("Objects")]
    public class AngryExportSystemList
    {
        [XmlElement(ElementName = "Object")]
        public ExportObject [] Objects { get; set; }

        Dictionary<string, ExportObject> _lookup;

        [XmlIgnore]
        public Dictionary<string, ExportObject> Lookup
        {
            get
            {
                try{

                _lookup ??= (Objects?.Length ?? 0) == 0 ?
                    new Dictionary<string, ExportObject>() :
                    Objects.ToDictionary(x => x?.BlenderName?.Value ?? string.Empty);
                return _lookup;
                }
                catch{
                    throw;
                }
            }
        }

        [XmlElement("AngryExportSystem_GenerateLightmap")]
        public GenerateLightmap GenerateLightmap { get; set; }
    }

    public class ExportObject
    {
        [XmlElement("AngryExportSystem_Render")]
        public Render Render {get; set;}

        [XmlElement("AngryExportSystem_Collider")]
        public Collider Collider {get; set;}
		
		[XmlElement("AngryExportSystem_PrefabLink")]
        public PrefabLink PrefabLink {get; set;}

		[XmlElement("AngryExportSystem_StaticFlags")]
        public StaticFlags StaticFlags {get; set;}

		[XmlElement("AngryExportSystem_LightmapScale")]
        public LightmapScale LightmapScale {get; set;}

		[XmlElement("AngryExportSystem_Export_Object")]
        public Export Export {get; set;}

        [XmlElement("blender_name")]
        public BlenderName BlenderName { get; set; }
    }

    public class GenerateLightmap
    {
        [XmlAttribute("value")]
        public bool Value { get; set; }
    }

    public class BlenderName
    {
        [XmlAttribute("value")]
        public string Value { get; set;}
    }


    public class Render
    {
        [XmlAttribute("value")]
        public string Value { get; set; }
        public bool Enabled => Value == "True";
    }

    public class Export
    {
        [XmlAttribute("value")]
        public string Value { get; set; }
        public bool Enabled => Value == "True";
    }



    public class Collider
    {
        [XmlAttribute("value")]
        public string ColliderType { get; set; }
    }
	
	public class PrefabLink
	{
		[XmlAttribute("value")]
		public string PrefabPath {get; set;}
	}

    public class StaticFlags
    {
        [XmlElement("flag")]
        public string[] Flags;
    }

    public class LightmapScale
    {
        [XmlAttribute("value")]
        public float Scale { get; set; }
    }
}