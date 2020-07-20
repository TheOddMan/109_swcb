using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace swcb01.Models
{
    public class ImageModel
    {
        public int id { get; set; }
        public string name { get; set; }
        public string location { get; set; }

        public DateTime photoDate { get; set; }
        public string disasterYear { get; set; }
        public string disasterName { get; set; }
        public string description { get; set; }
    }
}