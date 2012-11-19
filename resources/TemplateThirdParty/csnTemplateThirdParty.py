# CSNake configuration of the Template Third Party

# CSNake imports
from csnAPIPublic import GetAPI
api = GetAPI("2.5.0")

# Definition of the template third party
templateTP = api.CreateThirdPartyProject("TemplateThirdParty")
templateTP.SetUseFilePath("%s/TemplateThirdParty/UseTemplateThirdParty.cmake" % templateTP.GetBuildFolder())
templateTP.SetConfigFilePath("%s/TemplateThirdParty/TemplateThirdPartyConfig.cmake" % templateTP.GetBuildFolder())

if api.GetCompiler().TargetIsWindows():
  templateTP.AddFilesToInstall( templateTP.Glob("lib/nameofyourdlldebug.dll"), debugOnly = 1)
  templateTP.AddFilesToInstall( templateTP.Glob("lib/nameofyourdllrelease.dll"), releaseOnly = 1)
