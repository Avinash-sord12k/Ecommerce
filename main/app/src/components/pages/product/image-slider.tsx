import React from "react";

function ImageSlider() {
  return (
    <div className="grid gap-3 items-start">
      <div className="hidden md:flex gap-4 items-start">
        {[...Array(3)].map((_, idx) => (
          <button
            key={idx}
            className="border hover:border-gray-900 rounded-lg overflow-hidden transition-colors dark:hover:border-gray-50"
          >
            <img
              src="https://picsum.photos/200"
              alt={`Preview thumbnail ${idx + 1}`}
              width={100}
              height={100}
              className="aspect-square object-cover"
            />
            <span className="sr-only">View Image {idx + 1}</span>
          </button>
        ))}
      </div>
      <div className="grid gap-4 md:gap-10">
        <img
          src="https://picsum.photos/200"
          alt="Product Image"
          width={600}
          height={600}
          className="aspect-square object-cover border border-gray-200 w-full rounded-lg overflow-hidden dark:border-gray-800"
        />
        <div className="flex md:hidden items-start">
          {[...Array(5)].map((_, idx) => (
            <button
              key={idx}
              className="border hover:border-gray-900 rounded-lg overflow-hidden transition-colors dark:hover:border-gray-50"
            >
              <img
                src="https://picsum.photos/200"
                alt={`Preview thumbnail ${idx + 1}`}
                width={100}
                height={100}
                className="aspect-square object-cover"
              />
              <span className="sr-only">View Image {idx + 1}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ImageSlider;
