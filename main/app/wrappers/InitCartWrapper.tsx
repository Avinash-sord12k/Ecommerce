"use client";
import { useCreateCartMutation, useGetCartsQuery } from "@/store/api/cart";
import { useAppDispatch } from "@/store/hooks";
import { setDefaultCart } from "@/store/slices/cart";
import { useEffect } from "react";

export default function InitCartWrapper({ children }: { children: React.ReactNode }) {
  const { data, isSuccess: cartLoadingSuccess } = useGetCartsQuery({ get_items: false });
  const [createCart] = useCreateCartMutation();
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (cartLoadingSuccess) {
      console.log("🚀 ~ InitCartWrapper ~ data:", data);
      const noDefault = data.items.every((item) => item.name != "default");
      if (noDefault) {
        console.warn("default cart does not exist, creating one");
        const today = new Date();
        const reminder_date = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1).toISOString();
        createCart({ name: "default", reminder_date })
          .unwrap()
          .then((res) => {
            console.log("default cart created", res);
          })
          .catch((err) => {
            console.error("default cart creation failed", err);
          });
      } else {
        console.log("default cart already exists");
      }

      // now we can select the default cart
      const defaultCart = data.items.find((item) => item.name == "default");
      if (defaultCart) dispatch(setDefaultCart(defaultCart?.id));
      else console.error("default cart not found");
    }
  }, [data, cartLoadingSuccess]);

  return <>{children}</>;
}
