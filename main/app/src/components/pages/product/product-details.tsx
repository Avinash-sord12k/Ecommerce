import { SpecificProduct } from "@/app/(main)/product/[slug]/page";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { cutWords } from "@/lib/utils";
import { StarIcon } from "lucide-react";

function ProductDetails({ product }: { product: SpecificProduct }) {
  return (
    <div className="flex flex-col items-start h-full">
      {/* Mobile Header */}
      {/* <div className=" "> */}
      <div className="flex items-start">
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
                <StarIcon
                  key={idx}
                  className="w-5 h-5 fill-muted stroke-muted-foreground"
                />
              ))}
            </div>
          </div>
        </div>
        <div className="text-4xl font-bold ml-auto">$99</div>
      </div>

      {/* Form Section */}
      <form className="grid gap-4 md:gap-10 my-10">
        {/* Quantity Selection */}
        <div className="grid gap-2">
          <Label htmlFor="quantity" className="text-base">
            Quantity
          </Label>
          <Select defaultValue="1">
            <SelectTrigger className="w-24">
              <SelectValue placeholder="Select" />
            </SelectTrigger>
            <SelectContent>
              {[1, 2, 3, 4, 5].map((quantity) => (
                <SelectItem key={quantity} value={quantity.toString()}>
                  {quantity}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex w-full justify-stretch gap-4">
          <Button size="lg" className="w-full flex-1" variant={"outline"}>
            Add to cart
          </Button>
          <Button size="lg" className="w-full flex-1">
            Buy now
          </Button>
        </div>
      </form>
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
