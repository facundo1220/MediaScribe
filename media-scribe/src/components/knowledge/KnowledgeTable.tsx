import { TableData } from "../../types/table.types";
import { format } from "date-fns";
import { IoCheckmarkCircleSharp } from "react-icons/io5";
import { FaClock } from "react-icons/fa6";

function KnowledgeTable({ data }: TableData) {
  return (
    <div className=" overflow-x-auto shadow-md rounded-lg">
      <table className="w-full text-sm text-left rtl:text-right text-white">
        <thead className="text-xs text-white uppercase bg-[#26272F]">
          <tr>
            <th className="px-6 py-3">Name</th>
            <th className="px-6 py-3">Type</th>
            <th className="px-6 py-3">Creation date</th>
            <th className="px-6 py-3">Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr
              className="odd:bg-white odd:text-black  even:bg-gray-50 even:text-black  border-b "
              key={item.id}
            >
              <td className="px-6 py-3 justify-center">
                {item.knowledge_name}
              </td>
              <td className="px-6 py-3">{item.type.split("/")[0]}</td>
              <td className="px-6 py-3">
                {format(item.created_at, "dd/MM/yyyy")}
              </td>
              <td className="px-6 py-3">
                {item.ready === "True" ? (
                  <div className="flex gap-1 items-center">
                    Ready <IoCheckmarkCircleSharp size={18} color="green" />
                  </div>
                ) : (
                  <div className="flex gap-1 items-center">
                    Not Ready <FaClock size={20} color="#e9d700" />
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default KnowledgeTable;
