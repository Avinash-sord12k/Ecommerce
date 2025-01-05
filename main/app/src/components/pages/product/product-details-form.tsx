"use client";

import { SpecificProduct } from "@/app/(main)/products/[slug]/page";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAddItemsMutation } from "@/store/api/cart";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

export const ProductDetailsForm = ({ product }: { product: SpecificProduct }) => {
  const [quantity, setQuantity] = useState(1);
  const dispatch = useAppDispatch();
  const router = useRouter();
  const currentCartId = useAppSelector((state) => state.cart.defaultCart.id);
  const [addToCart, { isLoading: isAddingToCart }] = useAddItemsMutation();
  const handleClick = async () => {
    try {
      await addToCart({ product_id: product.id, quantity, cart_id: currentCartId }).unwrap();
      toast("Product add to cart", {
        description: `${quantity > 1 ? `${quantity} units of ` : ""}${product.name} has been added to your cart.`,
        action: {
          label: "View Cart",
          onClick: () => {
            router.push("/checkout");
          },
        },
      });
    } catch (error: any) {
      console.error("An error occurred: ", error);
      toast.error(`An error occurred. ${error?.data?.detail}`);
    }
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
