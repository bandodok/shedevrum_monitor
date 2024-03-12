import os


def remove_unused_libraries():
    """Удаляет лишние библиотеки после сборки приложения"""
    unused_libraries = [
        'opengl32sw.dll',
        'Qt63DAnimation.dll',
        'Qt63DCore.dll',
        'Qt63DExtras.dll',
        'Qt63DInput.dll',
        'Qt63DLogic.dll',
        'Qt63DQuick.dll',
        'Qt63DQuickAnimation.dll',
        'Qt63DQuickExtras.dll',
        'Qt63DQuickInput.dll',
        'Qt63DQuickRender.dll',
        'Qt63DQuickScene2D.dll',
        'Qt63DRender.dll',
        'Qt6DataVisualization.dll',
        'Qt6DataVisualizationQml.dll',
        'Qt6LabsAnimation.dll',
        'Qt6LabsSettings.dll',
        'Qt6LabsSharedImage.dll',
        'Qt6LabsWavefrontMesh.dll',
        'Qt6Multimedia.dll',
        'Qt6MultimediaQuick.dll',
        'Qt6Positioning.dll',
        'Qt6PositioningQuick.dll',
        'Qt6QmlLocalStorage.dll',
        'Qt6QmlXmlListModel.dll',
        'Qt6Quick3D.dll',
        'Qt6Quick3DAssetImport.dll',
        'Qt6Quick3DAssetUtils.dll',
        'Qt6Quick3DEffects.dll',
        'Qt6Quick3DHelpers.dll',
        'Qt6Quick3DParticles.dll',
        'Qt6Quick3DRuntimeRender.dll',
        'Qt6Quick3DUtils.dll',
        'Qt6QuickParticles.dll',
        'Qt6QuickShapes.dll',
        'Qt6QuickTest.dll',
        'Qt6RemoteObjects.dll',
        'Qt6RemoteObjectsQml.dll',
        'Qt6Scxml.dll',
        'Qt6ScxmlQml.dll',
        'Qt6Sensors.dll',
        'Qt6SensorsQuick.dll',
        'Qt6ShaderTools.dll',
        'Qt6Sql.dll',
        'Qt6StateMachine.dll',
        'Qt6StateMachineQml.dll',
        'Qt6Svg.dll',
        'Qt6Test.dll',
        'Qt6VirtualKeyboard.dll',
        'Qt6WebChannel.dll',
        'Qt6WebEngineCore.dll',
        'Qt6WebEngineQuick.dll',
        'Qt6WebEngineQuickDelegatesQml.dll',
        'Qt6WebSockets.dll',
    ]
    for lib in unused_libraries:
        try:
            os.remove(f'dist/ShedevrumMonitor/_internal/PySide6/{lib}')
        except FileNotFoundError:
            continue


def build_app():
    """Собирает основное приложение"""
    os.system('pyinstaller script.spec --noconfirm')


if __name__ == '__main__':
    build_app()
    # remove_unused_libraries()
