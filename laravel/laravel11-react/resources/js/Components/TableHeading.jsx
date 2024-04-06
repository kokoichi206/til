import { Children } from "react";
import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/24/solid";

export default function TableHeading({
    name,
    sortable = true,
    sort_field = null,
    sort_direction = null,
    sortChanged = () => {},
    children,
}) {
    return (
        <th onClick={(e) => sortChanged(name)}>
            <div className="px-3 py-2 flex items-center justify-between gap-1 cursor-pointer">
                {children}
                {sortable && (
                    <div>
                        <ChevronUpIcon
                            className={
                                "w-4 " +
                                (sort_field === name && sort_direction === "asc"
                                    ? "text-white "
                                    : "text-black")
                            }
                        />
                        {/* minus margin */}
                        <ChevronDownIcon
                            className={
                                "w-4 -mt-2 " +
                                (sort_field === name &&
                                sort_direction === "desc"
                                    ? "text-white "
                                    : "text-black")
                            }
                        />
                    </div>
                )}
            </div>
        </th>
    );
}
