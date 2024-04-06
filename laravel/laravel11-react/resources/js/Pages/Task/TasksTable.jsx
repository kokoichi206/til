import Pagination from "@/Components/Pagination";
import SelectInput from "@/Components/SelectInput";
import TableHeading from "@/Components/TableHeading";
import TextInput from "@/Components/TextInput";
import { TASK_STATUS_CLASS_MAP, TASK_STATUS_TEXT_MAP } from "@/constants";
import { Link, router } from "@inertiajs/react";

export default function TasksTable({
    tasks,
    queryParams,
    hideProjectColumn = false,
}) {
    const searchFieldChanged = (name, value) => {
        if (value) {
            queryParams[name] = value;
        } else {
            delete queryParams[name];
        }

        router.get(route("task.index"), queryParams);
    };

    const onKeyPress = (name, e) => {
        if (e.key === "Enter") {
            searchFieldChanged(name, e.target.value);
        }
    };

    const sortChanged = (name) => {
        // if already sorted by the same field
        if (name === queryParams.sort_field) {
            if (queryParams.sort_direction === "asc") {
                queryParams.sort_direction = "desc";
            } else {
                queryParams.sort_direction = "asc";
            }
        } else {
            queryParams.sort_field = name;
            queryParams.sort_direction = "asc";
        }

        router.get(route("task.index"), queryParams);
    };

    return (
        <>
            <div className="overflow-auto">
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-100 uppercase bg-gray-50 dark:bg-gray-700 border-gray-500">
                        <tr className="text-nowrap">
                            <TableHeading
                                name="id"
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                ID
                            </TableHeading>

                            <TableHeading
                                name="image_path"
                                sortable={false}
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Image
                            </TableHeading>

                            {!hideProjectColumn && (
                                <TableHeading
                                    name="project_name"
                                    sortable={false}
                                    sort_field={queryParams.sort_field}
                                    sort_direction={queryParams.sort_direction}
                                    sortChanged={sortChanged}
                                >
                                    Project Name
                                </TableHeading>
                            )}

                            <TableHeading
                                name="name"
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Name
                            </TableHeading>

                            <TableHeading
                                name="status"
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Status
                            </TableHeading>

                            <TableHeading
                                name="created_at"
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Created Date
                            </TableHeading>

                            <TableHeading
                                name="due_date"
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Due Date
                            </TableHeading>

                            <TableHeading
                                name="due_date"
                                sortable={false}
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Created By
                            </TableHeading>

                            <TableHeading
                                name="due_date"
                                sortable={false}
                                sort_field={queryParams.sort_field}
                                sort_direction={queryParams.sort_direction}
                                sortChanged={sortChanged}
                            >
                                Actions
                            </TableHeading>
                        </tr>
                    </thead>

                    {/* for search */}
                    <thead className="text-xs text-gray-100 uppercase bg-gray-50 dark:bg-gray-700 border-gray-500">
                        <tr className="text-nowrap">
                            <th className="px-3 py-2"></th>
                            <th className="px-3 py-2"></th>
                            {!hideProjectColumn && (
                                <th className="px-3 py-2"></th>
                            )}
                            <th className="px-3 py-2">
                                <TextInput
                                    className="w-full"
                                    defaultValue={queryParams.name}
                                    placeholder="Task Name"
                                    onBlur={(e) =>
                                        searchFieldChanged(
                                            "name",
                                            e.target.value
                                        )
                                    }
                                    onKeyPress={(e) => onKeyPress("name", e)}
                                />
                            </th>
                            <th className="px-3 py-2">
                                <SelectInput
                                    className="w-full"
                                    defaultValue={queryParams.status}
                                    onChange={(e) =>
                                        searchFieldChanged(
                                            "status",
                                            e.target.value
                                        )
                                    }
                                >
                                    <option value="">Select Status</option>
                                    <option value="pending">Pending</option>
                                    <option value="in_progress">
                                        In Progress
                                    </option>
                                    <option value="completed">Completed</option>
                                </SelectInput>
                            </th>
                            <th className="px-3 py-2"></th>
                            <th className="px-3 py-2"></th>
                            <th className="px-3 py-2"></th>
                            <th className="px-3 py-2"></th>
                        </tr>
                    </thead>

                    <tbody>
                        {tasks.data.map((task) => (
                            <tr
                                className="bg-white border-b dark:bg-gray-800"
                                key={task.id}
                            >
                                <td className="px-3 py-2">{task.id}</td>
                                <td className="px-3 py-2">
                                    <img src={task.image_path} width="69" />
                                </td>
                                {!hideProjectColumn && (
                                    <td className="px-3 py-2">
                                        {task.project.name}
                                    </td>
                                )}
                                <td className="px-3 py-2">{task.name}</td>
                                <td className="px-3 py-2">
                                    <span
                                        className={
                                            "px-2 py-1 rounded text-white " +
                                            TASK_STATUS_CLASS_MAP[task.status]
                                        }
                                    >
                                        {TASK_STATUS_TEXT_MAP[task.status]}
                                    </span>
                                </td>
                                <td className="px-3 py-2">{task.created_at}</td>
                                <td className="px-3 py-2 text-nowrap">
                                    {task.due_date}
                                </td>
                                <td className="px-3 py-2 text-nowrap">
                                    {task.createdBy.name}
                                </td>
                                <td className="px-3 py-2">
                                    <Link
                                        href={route("task.edit", task.id)}
                                        className="font-medium text-blue-600 hover:underline mx-1"
                                    >
                                        Edit
                                    </Link>
                                    <Link
                                        href={route("task.destroy", task.id)}
                                        className="font-medium text-red-600 hover:underline mx-1"
                                    >
                                        Delete
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <Pagination links={tasks.meta.links} />
        </>
    );
}
