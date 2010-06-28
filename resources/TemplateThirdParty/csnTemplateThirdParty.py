# Used to configure TemplateThirdParty
import csnBuild

templateThirdParty = csnBuild.Project("TemplateThirdParty", "third party")
templateThirdParty.pathsManager.useFilePath = "%s/TemplateThirdParty/UseTemplateThirdParty.cmake" % templateThirdParty.GetBuildFolder()
templateThirdParty.pathsManager.configFilePath = "%s/TemplateThirdParty/TemplateThirdPartyConfig.cmake" % templateThirdParty.GetBuildFolder()

templateThirdParty.AddFilesToInstall( templateThirdParty.Glob("lib/nameofyourdlldebug.dll"), _debugOnly = 1, _WIN32 = 1)
templateThirdParty.AddFilesToInstall( templateThirdParty.Glob("lib/nameofyourdllrelease.dll"), _releaseOnly = 1, _WIN32 = 1)
