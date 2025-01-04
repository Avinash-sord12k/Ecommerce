import { SpecificProduct } from "@/app/(main)/products/[slug]/page";
import { Separator } from "@/components/ui/separator";
import { cutWords } from "@/lib/utils";
import { StarIcon } from "lucide-react";
import { ProductDetailsForm } from "./product-details-form";

function ProductDetails({ product }: { product: SpecificProduct }) {
  return (
    <div className="flex flex-col items-start h-full">
      {/* Mobile Header */}
      {/* <div className=" "> */}
      <div className="flex items-start w-full">
        <div className="grid gap-4">
          <h1 className="font-bold text-2xl sm:text-3xl">{product?.name}</h1>
          <div>
            <p>60% combed ringspun cotton/40% polyester jersey tee.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-0.5">
              {[...Array(3)].map((_, idx) => (
                <StarIcon key={idx} className="w-5 h-5 fill-primary" />
              ))}
              {[...Array(2)].map((_, idx) => (
                <StarIcon key={idx} className="w-5 h-5 fill-muted stroke-muted-foreground" />
              ))}
            </div>
          </div>
        </div>
        <div className="text-4xl font-bold ml-auto">$99</div>
      </div>
      {/* Form Section */}
      <ProductDetailsForm product={product} />
      {/* </div> */}
      <Separator className="border-gray-200 dark:border-gray-800" />
      {/* Description */}
      <div className="grid gap-4 text-sm leading-loose">
        <p>{cutWords(product?.description ?? "", 200)}</p>
      </div>
    </div>
  );
}

export default ProductDetails;
