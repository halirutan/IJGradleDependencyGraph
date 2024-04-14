from typing import List

from config import Config, GradleTask


class MermaidRepresentation:
    mermaid_prefix = "%%{init: {\"flowchart\": {\"curve\": \"basis\"}} }%%\n" + "flowchart BT\n\n"

    def __init__(self, connections: set[tuple[str, str]], config: Config):
        self.connections = connections
        self.config = config

    def mermaid_representation_all_tasks(self, grouped: bool = True, include_all_tasks: bool = True) -> str:
        additional_tasks = None
        if include_all_tasks:
            additional_tasks = self.config.included_task_map.values()
        if grouped:
            return self._grouped_mermaid_representation(
                self.connections,
                additional_tasks=additional_tasks
            )
        else:
            return self._ungrouped_mermaid_representation(
                self.connections,
                additional_tasks=additional_tasks
            )

    def mermaid_representation_single_task(self, task_name: str) -> str:
        restricted_connections = {c for c in self.connections if c[0] == task_name}
        stack = [out[1] for out in restricted_connections]
        while len(stack) > 0:
            current_task = stack.pop()
            current_task_connections = {c for c in self.connections if c[0] == current_task}
            restricted_connections = restricted_connections.union(current_task_connections)
            for i in current_task_connections:
                if i[1] not in stack:
                    stack.append(i[1])

        # TODO: Currently not walking to the parents of task_name
        # stack = [task_name]
        # while len(stack) > 0:
        #     current_task = stack.pop()
        #     current_task_connections = {c for c in self.connections if c[1] == current_task}
        #     restricted_connections = restricted_connections.union(current_task_connections)
        #     for i in current_task_connections:
        #         if i[0] not in stack:
        #             stack.append(i[0])
        return self._grouped_mermaid_representation(restricted_connections, False)

    def _ungrouped_mermaid_representation(
            self,
            conn: set[tuple[str, str]],
            additional_tasks: List[GradleTask] = None) -> str:
        tasks = {e[0] for e in conn}
        tasks = tasks.union({e[1] for e in conn})
        if additional_tasks is not None:
            tasks = tasks.union([n.name for n in additional_tasks])

        node_definitions = []
        for task in tasks:
            task_name = self.config.get_task_identifier(task)
            task_style = self.config.get_task_style(task)
            node_definitions.append(f"    {task_name}:::{task_style.identifier}")

        node_connections = []
        for edge in MermaidRepresentation._sort_connections(conn):
            edge_name_0 = self.config.get_task_identifier(edge[0])
            edge_name_1 = self.config.get_task_identifier(edge[1])
            node_connections.append(f"    {edge_name_0} --> {edge_name_1}")
        node_connections.append("")

        return "\n".join(
            [MermaidRepresentation.mermaid_prefix] +
            [""] +
            node_definitions +
            [""] +
            node_connections +
            [""] +
            self.config.get_all_style_definitions() +
            [""] +
            self.config.get_all_click_anchors()
        )

    def _grouped_mermaid_representation(
            self,
            connections: set[tuple[str, str]],
            connect_only_groups: bool = True,
            additional_tasks: List[GradleTask] = None) -> str:

        tasks = {e[0] for e in connections}
        tasks = tasks.union({e[1] for e in connections})
        if additional_tasks is not None:
            tasks = tasks.union([n.name for n in additional_tasks])

        groups = {self.config.get_task_group(t) for t in tasks}

        mermaid_lines = []

        for g in groups:
            subgraph = [
                f"    subgraph {g.identifier}[\"{g.name}\"]",
                f"         direction LR",
                f"         style {g.identifier} fill:transparent"
            ]

            for task in [t for t in tasks if self.config.get_task_group(t) == g]:
                task_name = self.config.get_task_identifier(task)
                task_style = self.config.get_task_style(task)
                subgraph.append(f"        {task_name}:::{task_style.identifier}")

            for c in connections:
                g0 = self.config.get_task_group(c[0])
                g1 = self.config.get_task_group(c[1])
                if g0 == g and g1 == g:
                    identifier0 = self.config.get_task_identifier(c[0])
                    identifier1 = self.config.get_task_identifier(c[1])
                    subgraph.append(f"        {identifier0} --> {identifier1}")
            subgraph.append("    end")
            subgraph.append("")
            mermaid_lines += subgraph

        inter_group_connections = set()
        for edge in MermaidRepresentation._sort_connections(connections):
            g0 = self.config.get_task_group(edge[0])
            g1 = self.config.get_task_group(edge[1])
            if g0 != g1:
                if connect_only_groups:
                    group_name_0 = self.config.get_task_group(edge[0]).identifier
                    group_name_1 = self.config.get_task_group(edge[1]).identifier
                    inter_group_connections.add(f"    {group_name_0} --> {group_name_1}")
                else:
                    identifier0 = self.config.get_task_identifier(edge[0])
                    identifier1 = self.config.get_task_identifier(edge[1])
                    inter_group_connections.add(f"        {identifier0} --> {identifier1}")
        return "\n".join(
            [MermaidRepresentation.mermaid_prefix] +
            [""] +
            mermaid_lines +
            [""] +
            list(inter_group_connections) +
            [""] +
            self.config.get_all_style_definitions() +
            [""] +
            [self.config.get_task_click_anchor(t) for t in tasks
             if self.config.is_included_task(t) and self.config.included_task_map[t].has_url_anchor]
        )

    @staticmethod
    def _sort_connections(connections: set[tuple[str, str]]) -> list[tuple[str, str]]:
        """
        Sorts the connections `A --> B` based on the count of B's in all connections.

        :param connections: A set of tuples representing connections.
        :return: A sorted list of tuples representing connections.
        """
        values = [x[1] for x in connections]
        sorting_count = {x: values.count(x) for x in values}
        return sorted(connections, key=lambda x: sorting_count[x[1]])
