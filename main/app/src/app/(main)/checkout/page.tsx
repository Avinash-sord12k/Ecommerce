"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { updateQty } from "@/store/slices/cart";
import { MinusIcon, PlusIcon } from "lucide-react";
import Link from "next/link";
import React, { useMemo } from "react";

export default function CheckoutPage() {
  const cartData = useAppSelector((state) => state.cart.items);
  const dispatch = useAppDispatch();
  const { subTotal, taxes, total } = useMemo(() => {
    const subTotal = cartData?.reduce((acc, item) => acc + Number(item.product.computed_price) * item.quantity, 0);
    const taxes = subTotal * 0.08;
    const total = subTotal + taxes;
    return { subTotal, taxes, total };
  }, [cartData]);

  return (
    <React.Fragment>
      <main className="container mx-auto my-8 grid grid-cols-1 gap-8 md:grid-cols-[2fr_1fr]">
        <div>
          <h1 className="text-2xl font-bold">Your Cart</h1>
          <div className="mt-4 space-y-4">
            {cartData?.length > 0 ? (
              cartData?.map((singleItem, idx) => {
                return (
                  <div className="flex items-center gap-4 rounded-lg border bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-950">
                    <img
                      src={singleItem.product.thumbnail ?? singleItem.product.images?.[0] ?? "/images/vase_cropped.jpg"}
                      width={80}
                      height={80}
                      alt="Product Image"
                      className="rounded-md"
                      style={{ aspectRatio: "80/80", objectFit: "cover" }}
                    />
                    <div className="flex-1">
                      <h3 className="text-lg font-medium">{singleItem.product.name}</h3>
                      <p className="text-gray-500 dark:text-gray-400">{singleItem.product.description}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => {
                          dispatch(updateQty({ id: singleItem.id, quantity: singleItem.quantity - 1 }));
                        }}
                      >
                        <MinusIcon className="h-4 w-4" />
                      </Button>
                      <span>
                        {singleItem.quantity > 1 ? `${singleItem.quantity} units` : `${singleItem.quantity} unit`}
                      </span>
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => {
                          dispatch(updateQty({ id: singleItem.id, quantity: singleItem.quantity + 1 }));
                        }}
                      >
                        <PlusIcon className="h-4 w-4" />
                      </Button>
                    </div>
                    <div className="text-right font-medium">
                      {Number(singleItem.product.price)?.toLocaleString("en-IN", {
                        currency: "INR",
                        currencyDisplay: "narrowSymbol",
                        style: "currency",
                        currencySign: "accounting",
                      })}
                    </div>
                  </div>
                );
              })
            ) : (
              <>
                <div className="flex flex-col items-center justify-center">
                  <h3 className=" text-3xl font-semibold">Your cart is empty </h3>
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
