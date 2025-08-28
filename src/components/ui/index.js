import { cn } from "@/lib/utils"
import { useTheme } from "@/contexts/ThemeContext"

function Button({ className, variant = "default", size = "default", children, ...props }) {
  const baseClasses = "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
  
  const variants = {
    default: "bg-orange-600 text-white hover:bg-orange-700",
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
    ghost: "hover:bg-accent hover:text-accent-foreground",
  }
  
  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-9 rounded-md px-3",
    lg: "h-11 rounded-md px-8",
  }
  
  return (
    <button
      className={cn(baseClasses, variants[variant], sizes[size], className)}
      {...props}
    >
      {children}
    </button>
  )
}

function Card({ className, children, ...props }) {
  const { isDarkMode } = useTheme()
  
  return (
    <div
      className={cn(
        "rounded-lg border shadow-sm transition-colors duration-300", 
        isDarkMode 
          ? "bg-gray-800 border-gray-700 text-gray-100" 
          : "bg-white border-gray-200 text-gray-900",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

function CardHeader({ className, children, ...props }) {
  return (
    <div
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    >
      {children}
    </div>
  )
}

function CardTitle({ className, children, ...props }) {
  const { isDarkMode } = useTheme()
  
  return (
    <h3
      className={cn(
        "text-2xl font-semibold leading-none tracking-tight transition-colors duration-300",
        isDarkMode ? "text-gray-100" : "text-gray-900",
        className
      )}
      {...props}
    >
      {children}
    </h3>
  )
}

function CardDescription({ className, children, ...props }) {
  const { isDarkMode } = useTheme()
  
  return (
    <p
      className={cn(
        "text-sm transition-colors duration-300",
        isDarkMode ? "text-gray-400" : "text-gray-600",
        className
      )}
      {...props}
    >
      {children}
    </p>
  )
}

function CardContent({ className, children, ...props }) {
  return (
    <div className={cn("p-6 pt-0", className)} {...props}>
      {children}
    </div>
  )
}

export { Button, Card, CardHeader, CardTitle, CardDescription, CardContent }