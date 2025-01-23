import { ModalProps } from "../../types/modal.types";
import { IoClose } from "react-icons/io5";
import { useMedia } from "../../hooks/useMedia";
import { DataItem } from "../../types/table.types";
import { createSession } from "../../api/Chats";
import { useState } from "react";
import Loading from "../loading/Loading";
import { useNavigate } from "react-router-dom";

function ModalNewChat({ isOpen, onClose }: ModalProps) {
  const { knowledges } = useMedia();
  const [knowledge, setknowledge] = useState<string | null>(null);
  const [loading, setloading] = useState(false);
  const navigate = useNavigate();

  const data: DataItem[] = knowledges?.data || [];

  const handleClose = () => {
    onClose();
  };

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    try {
      event.preventDefault();
      setloading(true);
      const sessionId = await createSession({
        event,
        knowledge: `${knowledge}_extraction`,
      });
      handleClose();
      navigate(`/session/${sessionId}`);
    } catch (error) {
      console.log(error);
    } finally {
      setloading(false);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setknowledge(event.target.id);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <div className="fixed flex  inset-0 items-center justify-center bg-gray-700 bg-opacity-75">
          <div className="flex - flex-col bg-white w-1/4 h-1/3 rounded-xl p-5">
            <div className="flex justify-between items-center px-2 w-auto  h-14">
              <p className="text-xl font-semibold">New chat</p>
              <IoClose size={25} onClick={onClose} />
            </div>
            <form
              className="flex flex-col  gap-5 flex-1"
              onSubmit={handleFormSubmit}
            >
              <div className="px-2 flex flex-col gap-4 flex-1 ">
                <p className="text-md">
                  Choose your knowledge to start the chat
                </p>

                <div className="flex flex-col gap-2">
                  {data.map((item) => (
                    <div className=" flex items-center gap-2" key={item.id}>
                      {item.ready && (
                        <input
                          className="w-4 h-4 bg-orange-300 border-gray-300"
                          onChange={handleChange}
                          id={item.knowledge_name}
                          name="knowledgeItem"
                          type="radio"
                        />
                      )}

                      <label key={item.id}>{item.knowledge_name}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-end">
                <button
                  className="focus:outline-none text-white bg-red-700 hover:bg-red-800 rounded-lg text-sm px-5 py-2.5 me-2 mb-2 "
                  onClick={handleClose}
                >
                  cancel
                </button>
                <button
                  className="focus:outline-none text-white bg-green-700 hover:bg-green-800 rounded-lg text-sm px-5 py-2.5 me-2 mb-2 "
                  type="submit"
                >
                  start chat
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default ModalNewChat;
