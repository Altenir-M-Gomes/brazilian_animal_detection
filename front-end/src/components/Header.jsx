import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"

export default function Header() {
  return (
    <div className="w-full bg-[#1f3a56] h-14 flex justify-end items-center px-12">
      <Avatar className="h-9 w-9">
        <AvatarImage src="https://github.com/youruser.png" alt="User" />
        <AvatarFallback>U</AvatarFallback>
      </Avatar>
    </div>
  )
}
