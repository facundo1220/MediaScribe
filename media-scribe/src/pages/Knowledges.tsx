import { useEffect, useState } from "react";
import Button from "../components/button/Button";
import KnowledgeTable from "../components/knowledge/KnowledgeTable";
import ModalNewKnowledge from "../components/knowledge/ModalNewKnowledge";
import { getAllKnoweldges } from "../api/Knowledge";
import { useMedia } from "../hooks/useMedia";
import { TableData } from "../types/table.types";

function Knowledges() {
  const [isModalOpen, setisModalOpen] = useState(false);

  const { knowledges } = useMedia();

  const openModal = () => setisModalOpen(true);
  const closeModal = () => setisModalOpen(false);

  const data = knowledges ? knowledges.data : [];

  return (
    <div className=" flex flex-col gap-5">
      <div>
        <Button onclick={openModal} title="Add knowledge" />
      </div>

      <div>
        <KnowledgeTable data={data} />
      </div>

      <ModalNewKnowledge isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
}

export default Knowledges;
