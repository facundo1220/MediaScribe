interface ButtonArgs {
  title: string;
  onclick?: () => void;
}

function Button({ title, onclick }: ButtonArgs) {
  return (
    <button
      onClick={onclick}
      className="text-white bg-[#FF5F1F] hover:bg-orange-800 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2  focus:outline-none "
      type="button"
    >
      {title}
    </button>
  );
}

export default Button;
