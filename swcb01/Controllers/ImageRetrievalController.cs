﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using swcb01.Models;
using System.Web.Script.Serialization;
using Newtonsoft.Json;
using System.Diagnostics;
using System.Security;

namespace swcb01.Controllers
{
    public class ImageRetrievalController : Controller
    {
        ApplicationDbContext db = new ApplicationDbContext();

        // GET: ImageRetrieval
        public ActionResult Index()
        {
            
           return View();
                
        }

        [HttpPost]
        public ActionResult Index(HttpPostedFileBase file)
        {

            System.IO.DirectoryInfo di = new DirectoryInfo(Server.MapPath("~/SearchImage"));
            string sessionId = System.Web.HttpContext.Current.Session.SessionID;

            string fileName = null;
            if (file.ContentLength > 0)
            {
                fileName = sessionId + ".jpg";
                var path = Path.Combine(Server.MapPath("~/SearchImage"), fileName);
                file.SaveAs(path);
            }

            

            string resultString = run_cmd(fileName);


            RootObject result = null;
            result = JsonConvert.DeserializeObject<RootObject>(resultString);

            ViewBag.FileName = fileName;


            foreach(ImageModel i in result.Images)
            {
                string imageId = i.name.Replace(".jpg", "").Split(new string[] { "EvenID_" }, StringSplitOptions.None).Last();
                ImageDescription a = db.ImageDescription.FirstOrDefault(x => x.PhotoID == imageId);
                i.description = a.Description;
            }

            //var filepath = Path.Combine(Server.MapPath("~/SearchImage"), fileName);

            //if (System.IO.File.Exists(filepath))
            //{
            //    System.IO.File.Delete(path);
            //}


            return View(result.Images);
        }

       

        public string run_cmd(string fileName)
        {
            //var user = System.Security.Principal.WindowsIdentity.GetCurrent().User;
            //var userName = user.Translate(typeof(System.Security.Principal.NTAccount));

            ProcessStartInfo start = new ProcessStartInfo();
            //start.FileName = "D:/XinYu/Anaconda3/envs/apple/python.exe"; //LAB電腦python執行環境
            start.FileName = "C:/ProgramData/Anaconda3/envs/apple/python.exe"; //遠端伺服器python執行環境
            //string cmd = "D:/XinYu/109_swcbProject_server/pyScripts/02_02_01_AE_predictToAnnoyIndex.py";
            string cmd = Path.Combine(Server.MapPath("~/pyScripts"), "02_02_01_AE_predictToAnnoyIndex.py");
            start.Arguments = string.Format("\"{0}\" --qi \"{1}\"", cmd, fileName);
            //string passwordStr = "swater0"; //LAB電腦IIS密碼
            string passwordStr = "A056315739"; //遠端伺服器IIS密碼
            SecureString password = new SecureString();
            foreach (char c in passwordStr)
                password.AppendChar(c);
            start.Password = password;
            //start.UserName = "409LAB00";//LAB電腦IIS帳號
            start.UserName = "administrator"; //遠端伺服器IIS帳號

            start.UseShellExecute = false;// Do not use OS shell
            start.CreateNoWindow = true; // We don't need new window
            start.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            start.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
            
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string stderr = process.StandardError.ReadToEnd(); // Here are the exceptions from our Python script
                    string result = reader.ReadToEnd(); // Here is the result of StdOut(for example: print "test")
                    return result;
                }
            }
        }

        [HttpPost]
        public ActionResult Upload(HttpPostedFileBase file)
        {
            string fileName = null;
            if (file.ContentLength > 0)
            {
                

                fileName = Path.GetFileName(file.FileName);

                var path = Path.Combine(Server.MapPath("~/SearchImage"), fileName);
                file.SaveAs(path);
            }



            string result = run_cmd(fileName);


  
            return View();
            //return RedirectToAction("Index", new { imagesJson = result });
        }

        public class RootObject
        {
            public List<ImageModel> Images { get; set; }
        }
    }
}