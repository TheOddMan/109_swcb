using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;

namespace swcb01.Controllers
{
    public class ImageRetrievalAPIController : ApiController
    {

        public class fileDes
        {
            public string name { get; set; }
        }

        [HttpPost]
        public IHttpActionResult Index(fileDes f)
        {
            var mappedPath = System.Web.Hosting.HostingEnvironment.MapPath("~/SearchImage/" + f.name);

            //var filepath = Path.Combine(Server.MapPath("~/SearchImage"), f.name);

            if (System.IO.File.Exists(mappedPath))
            {
                System.IO.File.Delete(mappedPath);
            }
            return Ok("");
        }
    }
}
