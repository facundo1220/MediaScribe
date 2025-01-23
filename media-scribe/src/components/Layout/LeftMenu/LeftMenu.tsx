import MenuItem from "./MenuItem";
import { FaRegFile } from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { IoAddOutline } from "react-icons/io5";
import { AiOutlineMessage } from "react-icons/ai";
import ModalNewChat from "../../session/ModalNewChat";
import { useState } from "react";
import { useMedia } from "../../../hooks/useMedia";
import { DataChat } from "../../../types/chat.types";
import { PiOrangeDuotone } from "react-icons/pi";
import { GiFruitBowl } from "react-icons/gi";
import { PiTreePalmDuotone } from "react-icons/pi";

function LeftMenu() {
  const [isModalOpen, setisModalOpen] = useState(false);

  const { chats } = useMedia();

  const chatData: DataChat[] = chats?.data || [];
  const openModal = () => setisModalOpen(true);
  const closeModal = () => setisModalOpen(false);

  return (
    <div className="h-full space-y-3 pr-3 divide-y divide-[#26272F]">
      <NavLink to={"/"}>
        <div className="py-3 font-semibold flex gap-2 items-center justify-center text-white text-2xl">
          <PiOrangeDuotone size={26} color="#FF5F1F" />
          MediaScribe
        </div>
      </NavLink>

      <div className="py-3">
        <ul className="space-y-3">
          <li onClick={openModal}>
            <MenuItem title="New chat" iconIN={<PiTreePalmDuotone size={19} />} />
          </li>
          <li>
            <NavLink to={"/Knowledges"}>
              <MenuItem title="Knowledges" iconIN={<GiFruitBowl size={20} />} />
            </NavLink>
          </li>
        </ul>
      </div>
      <div className="py-3">
        <ul className="space-y-3">
          {chatData.map((item) => (
            <li key={item.id}>
              <NavLink to={`/session/${item.id}`}>
                <MenuItem
                  title={item.knowledge}
                  iconIN={<AiOutlineMessage size={15} />}
                  center={false}
                />
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
      <>
        <ModalNewChat isOpen={isModalOpen} onClose={closeModal} />
      </>
    </div>
  );
}

export default LeftMenu;
