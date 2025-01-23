import React from "react";

interface MenuItemInterface {
  title: string;
  iconIN: JSX.Element;
  center?: boolean;
}

function MenuItem({ title, iconIN, center = true }: MenuItemInterface) {
  return (
    <a
      className={`bg-[#26272F] px-3 h-12 rounded-xl flex gap-2 items-center ${
        center ? "justify-center" : "justify-start"
      }`}
    >
      {React.cloneElement(iconIN, { color: "#FF5F1F" })}
      <span className="text-white text-md truncate">{title}</span>
    </a>
  );
}

export default MenuItem;
