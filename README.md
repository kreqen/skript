# Skript

## Windows Build

This project includes a GitHub Actions workflow to automatically build a Windows executable (.exe) for the Skript application.

### How to download the Windows executable

1. Go to the [Actions](https://github.com/your-repo/skript/actions) tab in the GitHub repository.
2. Select the latest successful run of the **Build Windows Executable** workflow.
3. In the **Artifacts** section, download the `Skript-Windows-Executable` artifact.
4. Extract the downloaded ZIP file to get the `Skript.exe` executable.
5. Run `Skript.exe` on your Windows machine.

The executable is built using PyInstaller with all necessary dependencies bundled, including PySide6, matplotlib, and PIL.

For more details, see the `.github/workflows/build-windows.yml` file in the repository.