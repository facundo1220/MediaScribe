import { useState } from "react";
import { IoClose } from "react-icons/io5";
import { createKnowledge, indexKnowledge } from "../../api/Knowledge";
import { ModalProps } from "../../types/modal.types";
import Loading from "../loading/Loading";

function ModalNewKnowledge({ isOpen, onClose }: ModalProps) {
  const [showAdd, setshowAdd] = useState(false);
  const [file, setfile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [loading, setloading] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setshowAdd(true);
    const fileInput = event.target.files?.[0];
    if (fileInput) {
      setfile(fileInput);
      setFileName(fileInput.name.split(".")[0]);
    }
  };

  const handleClose = () => {
    setshowAdd(false);
    onClose();
  };

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    try {
      setloading(true);
      await createKnowledge({ event, file });

      indexKnowledge({ media_path: `${fileName}_extraction` });
      handleClose();
      window.location.reload();
    } catch (error) {
      console.log(error);
    } finally {
      setloading(false);
    }
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
          <div className="flex - flex-col bg-white w-1/4 h-1/4 rounded-xl p-5">
            <div className="flex justify-between items-center px-2 w-auto  h-14">
              <p className="text-xl font-semibold">Upload new knowledge</p>
              <IoClose size={25} onClick={onClose} />
            </div>
            <form
              className="flex flex-col  gap-5 flex-1"
              onSubmit={handleFormSubmit}
            >
              <div className="flex flex-1 items-center">
                <input
                  onChange={handleChange}
                  accept="audio/*,video/*"
                  type="file"
                  className="block w-full bg-gray-50 border border-gray-200 shadow-md rounded-lg text-sm  file:bg-gray-100 file:border-0 file:me-4 file:py-3 file:px-4
    "
                />
              </div>

              <div className="flex items-end">
                <button
                  className="focus:outline-none text-white bg-red-700 hover:bg-red-800 rounded-lg text-sm px-5 py-2.5 me-2 mb-2 "
                  onClick={handleClose}
                >
                  cancel
                </button>

                {showAdd ? (
                  <button
                    className="focus:outline-none text-white bg-green-700 hover:bg-green-800 rounded-lg text-sm px-5 py-2.5 me-2 mb-2 "
                    type="submit"
                  >
                    Add
                  </button>
                ) : null}
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default ModalNewKnowledge;
