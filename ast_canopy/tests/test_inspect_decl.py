# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from ast_canopy import parse_declarations_from_source
import os
import pathlib
import pytest

def get_decls(data_folder, filename):
    sourcefile = str(data_folder / filename)
    decls = parse_declarations_from_source(sourcefile, [sourcefile], "sm_80")
    return decls

def make_index(obj):
    return {item.name: item for item in obj}

def test_show_struct(data_folder):
    decls = get_decls(data_folder, "sample_inspect.cu")
    structs = make_index(decls.structs)

    for name, expected_repr in [
            ("Empty", "<Struct: 'Empty'>"),
            ("A"    , "<Struct: 'A'>"),
            ("B"    , "<Struct: 'B'>"),
        ]:
        S = structs[name]
        assert repr(S) == expected_repr

def test_show_structmethod(data_folder):
    decls = get_decls(data_folder, "sample_inspect.cu")
    structs = make_index(decls.structs)
    meths = make_index(structs["Methods"].methods)

    for name, expected_repr in [
            ("a", "<StructMethod: a() -> void>"),
            ("b", "<StructMethod: b(float, float) -> int>"),
            # ("c", "<StructMethod: c(int, ...) -> float>"), # elipsis not supported
        ]:
        M = meths[name]
        assert repr(M) == expected_repr

def test_show_templated_structmethod(data_folder):
    decls = get_decls(data_folder, "sample_inspect.cu")
    structs = make_index(decls.structs)
    tmeths = make_index(structs["Methods"].templated_methods)

    for name, expected_repr in [
            ("ta", "<FunctionTemplate: ta[T]() -> void>"),
            ("tb", "<FunctionTemplate: tb[T](T, int, float) -> T>"),
            ("tc", "<FunctionTemplate: tc[T](T) -> T>"),
            ("td", "<FunctionTemplate: td[T, U](T, U) -> void>"),
            ("te", "<FunctionTemplate: te[int]() -> void>"),
        ]:
        M = tmeths[name]
        assert repr(M) == expected_repr

def test_show_classtemplatemethod(data_folder):
    decls = get_decls(data_folder, "sample_inspect.cu")
    structs = make_index(decls.class_templates)
    meths = make_index(structs["TMethods"].methods)

    for name, expected_repr in [
            ("a", "<FunctionTemplate: a[T]() -> void>"),
            ("b", "<FunctionTemplate: TMethods[T].a[U](T, U) -> void>"), # possible rendering
        ]:
        M = meths[name]
        # import code
        # code.interact(local=dict(globals(), **locals()))
        #assert repr(M) == expected_repr

def test_show_templated_classtemplatemethod(data_folder):
    decls = get_decls(data_folder, "sample_inspect.cu")
    structs = make_index(decls.class_templates)
    meths = make_index(structs["TMethods"].templated_methods)

    for name, expected_repr in [
            ("ta", "<FunctionTemplate: a[U](T, U) -> void>"),
        ]:
        M = meths[name]
        import code
        code.interact(local=dict(globals(), **locals()))
        #assert repr(M) == expected_repr
