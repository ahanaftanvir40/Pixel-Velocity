'''OpenGL extension NV.internalformat_sample_query

This module customises the behaviour of the 
OpenGL.raw.GL.NV.internalformat_sample_query to provide a more 
Python-friendly API

Overview (from the spec)
	
	Some OpenGL implementations support modes of multisampling which have
	properties which are non-obvious to applications and/or which may not be
	standards conformant. The idea of non-conformant AA modes is not new,
	and is exposed in both GLX and EGL with config caveats and the
	GLX_NON_CONFORMANT_CONFIG for GLX and EGL_NON_CONFORMANT_CONFIG for EGL,
	or by querying the EGL_CONFORMANT attribute in newer versions of EGL.
	
	Both of these mechanisms operate on a per-config basis, which works as
	intended for window-based configs. However, with the advent of
	application-created FBOs, it is now possible to do all the multisample
	operations in an application-created FBO and never use a multisample
	window.
	
	This extension further extends the internalformat query mechanism
	(first introduced by ARB_internalformat_query and extended in
	ARB_internalformat_query2) and introduces a mechanism for a
	implementation to report properties of formats that may also be
	dependent on the number of samples.  This includes information
	such as whether the combination of format and samples should be
	considered conformant. This enables an implementation to report
	caveats which might apply to both window and FBO-based rendering
	configurations.
	
	Some NVIDIA drivers support multisample modes which are internally
	implemented as a combination of multisampling and automatic
	supersampling in order to obtain a higher level of anti-aliasing than
	can be directly supported by hardware. This extension allows those
	properties to be queried by an application with the MULTISAMPLES_NV,
	SUPERSAMPLE_SCALE_X_NV and SUPERSAMPLE_SCALE_Y_NV properties. For
	example, a 16xAA mode might be implemented by using 4 samples and
	up-scaling by a factor of 2 in each of the x- and y-dimensions.
	In this example, the driver might report MULTSAMPLES_NV of 4,
	SUPERSAMPLE_SCALE_X_NV of 2, SUPERSAMPLE_SCALE_Y_NV of 2 and
	CONFORMANT_NV of FALSE.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/internalformat_sample_query.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.NV.internalformat_sample_query import *
from OpenGL.raw.GL.NV.internalformat_sample_query import _EXTENSION_NAME

def glInitInternalformatSampleQueryNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

# INPUT glGetInternalformatSampleivNV.params size not checked against bufSize
glGetInternalformatSampleivNV=wrapper.wrapper(glGetInternalformatSampleivNV).setInputArraySize(
    'params', None
)
### END AUTOGENERATED SECTION