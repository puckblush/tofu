@echo off
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\real-time protection" /v DisableRealtimeMonitoring /d 1 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\real-time protection" /v LocalSettingOverrideDisableRealTimeMonitoring /d 1 /f
powershell "Set-MpPreference -DisableRea $true"
