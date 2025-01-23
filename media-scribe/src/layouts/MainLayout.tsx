import LeftMenu from "../components/Layout/LeftMenu/LeftMenu";

interface props {
  children: JSX.Element | JSX.Element[];
}

function MainLayout({ children }: props) {
  return (
    <div className="bg-[#1B1C21]">
      <div className="flex h-screen  p-3 ">
        <div className="w-48">
          <LeftMenu />
        </div>
        <div className="bg-white grow rounded-3xl p-5">{children}</div>
      </div>
    </div>
  );
}

export default MainLayout;
