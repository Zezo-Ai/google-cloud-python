#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse
import os
import libcst as cst
import pathlib
import sys
from typing import (Any, Callable, Dict, List, Sequence, Tuple)


def partition(
    predicate: Callable[[Any], bool],
    iterator: Sequence[Any]
) -> Tuple[List[Any], List[Any]]:
    """A stable, out-of-place partition."""
    results = ([], [])

    for i in iterator:
        results[int(predicate(i))].append(i)

    # Returns trueList, falseList
    return results[1], results[0]


class network_servicesCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'create_authz_extension': ('parent', 'authz_extension_id', 'authz_extension', 'request_id', ),
        'create_endpoint_policy': ('parent', 'endpoint_policy_id', 'endpoint_policy', ),
        'create_gateway': ('parent', 'gateway_id', 'gateway', ),
        'create_grpc_route': ('parent', 'grpc_route_id', 'grpc_route', ),
        'create_http_route': ('parent', 'http_route_id', 'http_route', ),
        'create_lb_route_extension': ('parent', 'lb_route_extension_id', 'lb_route_extension', 'request_id', ),
        'create_lb_traffic_extension': ('parent', 'lb_traffic_extension_id', 'lb_traffic_extension', 'request_id', ),
        'create_mesh': ('parent', 'mesh_id', 'mesh', ),
        'create_service_binding': ('parent', 'service_binding_id', 'service_binding', ),
        'create_service_lb_policy': ('parent', 'service_lb_policy_id', 'service_lb_policy', ),
        'create_tcp_route': ('parent', 'tcp_route_id', 'tcp_route', ),
        'create_tls_route': ('parent', 'tls_route_id', 'tls_route', ),
        'create_wasm_plugin': ('parent', 'wasm_plugin_id', 'wasm_plugin', ),
        'create_wasm_plugin_version': ('parent', 'wasm_plugin_version_id', 'wasm_plugin_version', ),
        'delete_authz_extension': ('name', 'request_id', ),
        'delete_endpoint_policy': ('name', ),
        'delete_gateway': ('name', ),
        'delete_grpc_route': ('name', ),
        'delete_http_route': ('name', ),
        'delete_lb_route_extension': ('name', 'request_id', ),
        'delete_lb_traffic_extension': ('name', 'request_id', ),
        'delete_mesh': ('name', ),
        'delete_service_binding': ('name', ),
        'delete_service_lb_policy': ('name', ),
        'delete_tcp_route': ('name', ),
        'delete_tls_route': ('name', ),
        'delete_wasm_plugin': ('name', ),
        'delete_wasm_plugin_version': ('name', ),
        'get_authz_extension': ('name', ),
        'get_endpoint_policy': ('name', ),
        'get_gateway': ('name', ),
        'get_gateway_route_view': ('name', ),
        'get_grpc_route': ('name', ),
        'get_http_route': ('name', ),
        'get_lb_route_extension': ('name', ),
        'get_lb_traffic_extension': ('name', ),
        'get_mesh': ('name', ),
        'get_mesh_route_view': ('name', ),
        'get_service_binding': ('name', ),
        'get_service_lb_policy': ('name', ),
        'get_tcp_route': ('name', ),
        'get_tls_route': ('name', ),
        'get_wasm_plugin': ('name', 'view', ),
        'get_wasm_plugin_version': ('name', ),
        'list_authz_extensions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_endpoint_policies': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_gateway_route_views': ('parent', 'page_size', 'page_token', ),
        'list_gateways': ('parent', 'page_size', 'page_token', ),
        'list_grpc_routes': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_http_routes': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_lb_route_extensions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_lb_traffic_extensions': ('parent', 'page_size', 'page_token', 'filter', 'order_by', ),
        'list_meshes': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_mesh_route_views': ('parent', 'page_size', 'page_token', ),
        'list_service_bindings': ('parent', 'page_size', 'page_token', ),
        'list_service_lb_policies': ('parent', 'page_size', 'page_token', ),
        'list_tcp_routes': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_tls_routes': ('parent', 'page_size', 'page_token', 'return_partial_success', ),
        'list_wasm_plugins': ('parent', 'page_size', 'page_token', ),
        'list_wasm_plugin_versions': ('parent', 'page_size', 'page_token', ),
        'update_authz_extension': ('update_mask', 'authz_extension', 'request_id', ),
        'update_endpoint_policy': ('endpoint_policy', 'update_mask', ),
        'update_gateway': ('gateway', 'update_mask', ),
        'update_grpc_route': ('grpc_route', 'update_mask', ),
        'update_http_route': ('http_route', 'update_mask', ),
        'update_lb_route_extension': ('lb_route_extension', 'update_mask', 'request_id', ),
        'update_lb_traffic_extension': ('lb_traffic_extension', 'update_mask', 'request_id', ),
        'update_mesh': ('mesh', 'update_mask', ),
        'update_service_binding': ('service_binding', 'update_mask', ),
        'update_service_lb_policy': ('service_lb_policy', 'update_mask', ),
        'update_tcp_route': ('tcp_route', 'update_mask', ),
        'update_tls_route': ('tls_route', 'update_mask', ),
        'update_wasm_plugin': ('wasm_plugin', 'update_mask', ),
    }

    def leave_Call(self, original: cst.Call, updated: cst.Call) -> cst.CSTNode:
        try:
            key = original.func.attr.value
            kword_params = self.METHOD_TO_PARAMS[key]
        except (AttributeError, KeyError):
            # Either not a method from the API or too convoluted to be sure.
            return updated

        # If the existing code is valid, keyword args come after positional args.
        # Therefore, all positional args must map to the first parameters.
        args, kwargs = partition(lambda a: not bool(a.keyword), updated.args)
        if any(k.keyword.value == "request" for k in kwargs):
            # We've already fixed this file, don't fix it again.
            return updated

        kwargs, ctrl_kwargs = partition(
            lambda a: a.keyword.value not in self.CTRL_PARAMS,
            kwargs
        )

        args, ctrl_args = args[:len(kword_params)], args[len(kword_params):]
        ctrl_kwargs.extend(cst.Arg(value=a.value, keyword=cst.Name(value=ctrl))
                           for a, ctrl in zip(ctrl_args, self.CTRL_PARAMS))

        request_arg = cst.Arg(
            value=cst.Dict([
                cst.DictElement(
                    cst.SimpleString("'{}'".format(name)),
cst.Element(value=arg.value)
                )
                # Note: the args + kwargs looks silly, but keep in mind that
                # the control parameters had to be stripped out, and that
                # those could have been passed positionally or by keyword.
                for name, arg in zip(kword_params, args + kwargs)]),
            keyword=cst.Name("request")
        )

        return updated.with_changes(
            args=[request_arg] + ctrl_kwargs
        )


def fix_files(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    *,
    transformer=network_servicesCallTransformer(),
):
    """Duplicate the input dir to the output dir, fixing file method calls.

    Preconditions:
    * in_dir is a real directory
    * out_dir is a real, empty directory
    """
    pyfile_gen = (
        pathlib.Path(os.path.join(root, f))
        for root, _, files in os.walk(in_dir)
        for f in files if os.path.splitext(f)[1] == ".py"
    )

    for fpath in pyfile_gen:
        with open(fpath, 'r') as f:
            src = f.read()

        # Parse the code and insert method call fixes.
        tree = cst.parse_module(src)
        updated = tree.visit(transformer)

        # Create the path and directory structure for the new file.
        updated_path = out_dir.joinpath(fpath.relative_to(in_dir))
        updated_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the updated source file at the corresponding path.
        with open(updated_path, 'w') as f:
            f.write(updated.code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Fix up source that uses the network_services client library.

The existing sources are NOT overwritten but are copied to output_dir with changes made.

Note: This tool operates at a best-effort level at converting positional
      parameters in client method calls to keyword based parameters.
      Cases where it WILL FAIL include
      A) * or ** expansion in a method call.
      B) Calls via function or method alias (includes free function calls)
      C) Indirect or dispatched calls (e.g. the method is looked up dynamically)

      These all constitute false negatives. The tool will also detect false
      positives when an API method shares a name with another method.
""")
    parser.add_argument(
        '-d',
        '--input-directory',
        required=True,
        dest='input_dir',
        help='the input directory to walk for python files to fix up',
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        required=True,
        dest='output_dir',
        help='the directory to output files fixed via un-flattening',
    )
    args = parser.parse_args()
    input_dir = pathlib.Path(args.input_dir)
    output_dir = pathlib.Path(args.output_dir)
    if not input_dir.is_dir():
        print(
            f"input directory '{input_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if not output_dir.is_dir():
        print(
            f"output directory '{output_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if os.listdir(output_dir):
        print(
            f"output directory '{output_dir}' is not empty",
            file=sys.stderr,
        )
        sys.exit(-1)

    fix_files(input_dir, output_dir)
