

generate_from_proto: raft.proto
	python3 -m grpc_tools.protoc raft.proto --proto_path=. --python_out=. --grpc_python_out=.

.PHONY: generate_from_proto