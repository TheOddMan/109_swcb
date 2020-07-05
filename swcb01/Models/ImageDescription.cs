namespace swcb01.Models
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("ImageDescription")]
    public partial class ImageDescription
    {
        public double? Editable { get; set; }

        public double? Angle { get; set; }

        [StringLength(255)]
        public string Location { get; set; }

        [StringLength(255)]
        public string EventID { get; set; }

        [StringLength(255)]
        public string OwnerId { get; set; }

        [StringLength(255)]
        public string DisasterYear { get; set; }

        [StringLength(255)]
        public string DisasterName { get; set; }

        public double? Lat { get; set; }

        public double? Lng { get; set; }

        [StringLength(255)]
        public string PhotoDate { get; set; }

        [StringLength(255)]
        public string FileName { get; set; }

        [StringLength(255)]
        public string Source { get; set; }

        [StringLength(255)]
        public string Landmark { get; set; }

        [StringLength(255)]
        public string Description { get; set; }

        [StringLength(255)]
        public string Note { get; set; }

        [StringLength(255)]
        public string Note2 { get; set; }

        [StringLength(255)]
        public string License { get; set; }

        [StringLength(255)]
        public string vote { get; set; }

        public double? ViewCount { get; set; }

        [StringLength(255)]
        public string PhotoType { get; set; }

        public double? MediaType { get; set; }

        [StringLength(255)]
        public string VideoUrl { get; set; }

        [StringLength(255)]
        public string Link { get; set; }

        [StringLength(255)]
        public string ProcessUnit { get; set; }

        public bool NeedToInvestigate { get; set; }

        [StringLength(255)]
        public string ShowPublic { get; set; }

        [StringLength(255)]
        public string Name { get; set; }

        [StringLength(255)]
        public string Tags { get; set; }

        [Key]
        [StringLength(255)]
        public string PhotoID { get; set; }
    }
}
