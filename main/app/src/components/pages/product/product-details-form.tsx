"use client";

import { SpecificProduct } from "@/app/(main)/products/[slug]/page";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAppDispatch } from "@/store/hooks";
import { addToCart } from "@/store/slices/cart";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

export const ProductDetailsForm = ({ product }: { product: SpecificProduct }) => {
  const [quantity, setQuantity] = useState(1);
  const dispatch = useAppDispatch();
  const router = useRouter();
  const handleClick = () => {
    dispatch(
      addToCart({
        product,
        quantity,
      })
    );
    toast("Product add to cart", {
      description: `${quantity > 1 ? `${quantity} units of ` : ""}${product.name} has been added to your cart.`,
      action: {
        label: "View Cart",
        onClick: () => {
          // Navigate to cart page
          router.push("/checkout");
        },
      },
    });
  };

  return (
    <form className="grid gap-4 md:gap-10 my-10">
      {/* Quantity Selection */}
      <div className="grid gap-2">
        <Label htmlFor="quantity" className="text-base">
          Quantity
        </Label>
        <Select
          defaultValue="1"
          onValueChange={(value) => {
            setQuantity(Number(value));
          }}
        >
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
        <Button onClick={handleClick} type="button" size="lg" className="w-full flex-1" variant={"outline"}>
          Add to cart
        </Button>
        <Button size="lg" className="w-full flex-1">
          Buy now
        </Button>
      </div>
    </form>
  );
};
