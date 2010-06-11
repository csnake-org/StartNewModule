# Used to configure TemplateThirdParty
import csnBuild

templateThirdParty = csnBuild.Project("TemplateThirdParty", "third party")
if csnBuild.version >= 2.22:
    templateThirdParty.pathsManager.useFilePath = "%s/TemplateThirdParty/UseTemplateThirdParty.cmake" % templateThirdParty.context.GetThirdPartyBuildFolder()
    templateThirdParty.pathsManager.configFilePath = "%s/TemplateThirdParty/TemplateThirdPartyConfig.cmake" % templateThirdParty.context.GetThirdPartyBuildFolder()
else:
    templateThirdParty.pathsManager.useFilePath = "%s/TemplateThirdParty/UseTemplateThirdParty.cmake" % templateThirdParty.context.thirdPartyBuildFolder
    templateThirdParty.pathsManager.configFilePath = "%s/TemplateThirdParty/TemplateThirdPartyConfig.cmake" % templateThirdParty.context.thirdPartyBuildFolder

templateThirdParty.AddFilesToInstall( templateThirdParty.Glob("lib/nameofyourdlldebug.dll"), _debugOnly = 1, _WIN32 = 1)
templateThirdParty.AddFilesToInstall( templateThirdParty.Glob("lib/nameofyourdllrelease.dll"), _releaseOnly = 1, _WIN32 = 1)
