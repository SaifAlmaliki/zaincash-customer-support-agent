"use client";

import { motion } from "motion/react";
import { cn } from "@/lib/utils";

export function ShimmerText({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  return (
    <motion.span
      className={cn(
        "inline-block bg-[length:200%_100%] bg-clip-text text-transparent",
        "bg-[linear-gradient(110deg,#6b7280_35%,#111827_50%,#6b7280_65%)]",
        "dark:bg-[linear-gradient(110deg,#9ca3af_35%,#f9fafb_50%,#9ca3af_65%)]",
        className,
      )}
      animate={{ backgroundPosition: ["100% 0", "-100% 0"] }}
      transition={{ duration: 1.6, repeat: Infinity, ease: "linear" }}
    >
      {text}
    </motion.span>
  );
}
