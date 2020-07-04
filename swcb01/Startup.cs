using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(swcb01.Startup))]
namespace swcb01
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
