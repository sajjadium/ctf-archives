import { Link } from "wouter";

import { cn } from "@/lib/utils";

export default function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <nav
      className={cn("flex items-center space-x-4 lg:space-x-6", className)}
      {...props}
    >
      <Link
        href="/hacktivity"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Hacktivity
      </Link>
      <Link
        href="/programs"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Programs
      </Link>
    </nav>
  );
}
