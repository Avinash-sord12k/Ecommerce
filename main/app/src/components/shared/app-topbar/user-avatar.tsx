"use client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useLogoutMutation, useSessionQuery } from "@/store/api/auth";
import Link from "next/link";

export default function UserAvatar() {
  const { data, isLoading } = useSessionQuery();
  console.log("🚀 ~ UserAvatar ~ data:", data);
  const [logout] = useLogoutMutation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      {data ? (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Avatar>
              <AvatarImage src="" />
              <AvatarFallback delayMs={80}>
                <div className="capitalize">{data?.username?.slice(0, 2)}</div>
              </AvatarFallback>
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-48">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Checkout</DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuLabel>Manage</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Orders</DropdownMenuItem>
              <DropdownMenuItem>Cart</DropdownMenuItem>
              <DropdownMenuItem>Wishlist</DropdownMenuItem>
              <DropdownMenuItem>Address</DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link
                href={"#"}
                onClick={() => {
                  logout().then(() => {
                    window.location.reload();
                  });
                }}
              >
                Log out
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ) : (
        <a href="/login">Login</a>
      )}
    </>
  );
}
