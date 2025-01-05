"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { useGetCartsQuery } from "@/store/api/cart";
import { useGetProductsQuery } from "@/store/api/products";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { setDefaultCart } from "@/store/slices/cart";
import { DropdownMenu, DropdownMenuTrigger } from "@radix-ui/react-dropdown-menu";
import { SelectGroup } from "@radix-ui/react-select";
// import { updateQty } from "@/store/slices/cart";
import { MinusIcon, PlusIcon } from "lucide-react";
import Link from "next/link";
import React, { useMemo } from "react";

export default function CheckoutPage() {
  const { data: cartData, isLoading: isCartLoading } = useGetCartsQuery({
    get_items: true,
  });

  const currentCartId = useAppSelector((state) => state.cart.defaultCart);
  console.log("🚀 ~ CheckoutPage ~ currentCartId:", currentCartId);
  const currentCart = currentCartId ? cartData?.items.find((item) => item.id === currentCartId?.id) : cartData?.items?.[0];

  const currectCartProductIds = currentCart?.items?.map((item) => item.product_id).join(", ");
  console.log("🚀 ~ CheckoutPage ~ currectCartProductIds:", currectCartProductIds);
  const { data: productData, isLoading: isProductsLoading } = useGetProductsQuery(
    {
      ids: currectCartProductIds,
      page_size: currentCart?.items?.length,
    },
    {
      skip: !currectCartProductIds,
    }
  );
  const products = productData?.items;

  const dispatch = useAppDispatch();
  const { subTotal, taxes, total } = useMemo(() => {
    const subTotal =
      productData?.items?.reduce((acc, item) => {
        const itemQuantity = currentCart?.items?.find((cartItem) => cartItem.product_id === item.id)?.quantity ?? 0;
        return acc + Number(item.computed_price) * itemQuantity;
      }, 0) ?? 0;
    const taxes = subTotal * 0.08;
    const total = subTotal + taxes;
    return { subTotal, taxes, total };
  }, [currentCart?.id, productData?.items]);

  return (
    <React.Fragment>
      <main className="container mx-auto my-8 grid grid-cols-1 gap-8 md:grid-cols-[2fr_1fr]">
        <div>
          <div className=" flex justify-between items-center">
            <h1 className="text-2xl font-bold">Your Cart</h1>
            <Select
              name="cart"
              onValueChange={(value) => {
                dispatch(setDefaultCart(Number(value)));
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="default" defaultValue={currentCartId.id} />
              </SelectTrigger>
              <SelectContent>
                {cartData?.items?.map((item) => (
                  <SelectItem key={item.id} value={String(item.id)}>
                    {item.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="mt-4 space-y-4">
            {currectCartProductIds && products?.length
              ? products?.map((singleItem, idx) => {
                  const cartItem = currentCart?.items?.find((item) => item.product_id === singleItem.id);
                  return (
                    cartItem && (
                      <div
                        key={idx}
                        className="flex items-center gap-4 rounded-lg border bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-950"
                      >
                        <img
                          src={singleItem.thumbnail ?? singleItem.images?.[0] ?? "/images/vase_cropped.jpg"}
                          width={80}
                          height={80}
                          alt="Product Image"
                          className="rounded-md"
                          style={{ aspectRatio: "80/80", objectFit: "cover" }}
                        />
                        <div className="flex-1">
                          <h3 className="text-lg font-medium">{singleItem.name}</h3>
                          <p className="text-gray-500 dark:text-gray-400">{singleItem.description}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button
                            variant="outline"
                            size="icon"
                            onClick={() => {
                              // dispatch(updateQty({ id: singleItem.id, quantity: singleItem.quantity - 1 }));
                            }}
                          >
                            <MinusIcon className="h-4 w-4" />
                          </Button>
                          <span>{cartItem?.quantity > 1 ? `${cartItem.quantity} units` : `${cartItem.quantity} unit`}</span>
                          <Button
                            variant="outline"
                            size="icon"
                            onClick={() => {
                              // dispatch(updateQty({ id: singleItem.id, quantity: singleItem.quantity + 1 }));
                            }}
                          >
                            <PlusIcon className="h-4 w-4" />
                          </Button>
                        </div>
                        <div className="text-right font-medium">
                          {Number(singleItem.price)?.toLocaleString("en-IN", {
                            currency: "INR",
                            currencyDisplay: "narrowSymbol",
                            style: "currency",
                            currencySign: "accounting",
                          })}
                        </div>
                      </div>
                    )
                  );
                })
              : !(isProductsLoading && isCartLoading) && (
                  <>
                    <div className="flex flex-col items-center justify-center py-10">
                      <h3 className=" text-3xl font-semibold mb-2">{currentCart?.name} cart is empty </h3>
                      <p className="text-gray-500 mb-10">No items in your cart</p>
                      <Button size="lg" asChild>
                        <Link href="/products">Shop Now</Link>
                      </Button>
                    </div>
                  </>
                )}
          </div>
        </div>
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between">
                <span>Subtotal</span>
                <span>
                  {Number(subTotal)?.toLocaleString("en-IN", {
                    currency: "INR",
                    currencyDisplay: "narrowSymbol",
                    style: "currency",
                    currencySign: "accounting",
                  })}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Taxes</span>
                <span>
                  {Number(taxes)?.toLocaleString("en-IN", {
                    currency: "INR",
                    currencyDisplay: "narrowSymbol",
                    style: "currency",
                    currencySign: "accounting",
                  })}
                </span>
              </div>
              <Separator />
              <div className="flex items-center justify-between font-medium">
                <span>Total</span>
                <span>
                  {Number(total)?.toLocaleString("en-IN", {
                    currency: "INR",
                    currencyDisplay: "narrowSymbol",
                    style: "currency",
                    currencySign: "accounting",
                  })}
                </span>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Shipping &amp; Payment</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" placeholder="John Doe" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" placeholder="john@example.com" />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Textarea id="address" placeholder="123 Main St, Anytown USA" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="payment">Payment Method</Label>
                <Select name="payment">
                  <SelectTrigger>
                    <SelectValue placeholder="Select payment method" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="credit-card">Credit Card</SelectItem>
                    <SelectItem value="paypal">PayPal</SelectItem>
                    <SelectItem value="apple-pay">Apple Pay</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
            <CardFooter>
              <Button className="w-full">Place Order</Button>
            </CardFooter>
          </Card>
        </div>
      </main>
    </React.Fragment>
  );
}
