# C++ CPU acceleration layer -- see README.md's "Acceleration Layer" section.
#
# Builds one pybind11 extension module, `_core_accelerators` (leading underscore: it is
# an implementation detail, re-exported by __init__.py in this directory under the
# public name `core_accelerators`), from text_ops.cpp and nlp_accel.cpp. This is
# entirely optional: nlp_pipeline.native_accel imports the compiled module if it is on
# the Python path and falls back to a pure-Python implementation if it is not, so
# nothing in the pipeline requires this to have been built. Build it when large-document
# runtime becomes a bottleneck (see native_accel.py's module docstring for the two
# functions this actually speeds up).
#
# Usage:
#   pip install pybind11
#   cmake -S src/core_accelerators -B src/core_accelerators/build
#   cmake --build src/core_accelerators/build
# The extension is placed directly in src/core_accelerators/ (this directory, alongside
# __init__.py), which is already on sys.path wherever the rest of nlp_pipeline is
# importable (main.py and tests/conftest.py both `sys.path.insert(0, ".../src")`), so
# `import core_accelerators` then just works -- no separate install step.
#
# The extension is named `_core_accelerators`, not `core_accelerators`, on purpose: this
# directory is itself importable as the `core_accelerators` package (see __init__.py),
# and a compiled module sharing that exact name, nested one level inside a directory of
# the same name, loses to the directory in Python's import resolution -- `import
# core_accelerators` would silently resolve to the (function-less) namespace package
# instead of the extension. The underscore prefix sidesteps that collision entirely.

cmake_minimum_required(VERSION 3.15)
project(core_accelerators LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core_accelerators
  bindings.cpp
  text_ops.cpp
  nlp_accel.cpp
)

target_compile_options(_core_accelerators PRIVATE -O3 -Wall -Wextra)

# Drop the built extension next to this CMakeLists.txt, not into the build tree, so it
# lands exactly where __init__.py's `from ._core_accelerators import ...` looks for it.
set_target_properties(_core_accelerators PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
)
