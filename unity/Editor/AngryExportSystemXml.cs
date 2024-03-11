using System.Xml.Serialization;
using UnityEditor;

namespace AngryLabs.AngryExportSystem
{
    [XmlRoot("Components")]
    public class AngryExportSystemXml
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

    }


    public class Render
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