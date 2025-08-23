export default function TestPage() {
  return (
    <div className="min-h-screen bg-red-500 p-8">
      <h1 className="text-4xl font-bold text-white mb-8">CSS DEBUG TEST PAGE</h1>
      
      <div className="bg-blue-500 p-4 m-4 rounded-lg">
        <p className="text-yellow-300 text-xl">If you can see colors, Tailwind is working!</p>
      </div>
      
      <div className="bg-green-500 p-4 m-4 rounded-lg">
        <p className="text-white text-lg">This should be green with white text</p>
      </div>
      
      <div className="bg-purple-600 p-4 m-4 rounded-lg">
        <p className="text-white text-lg">This should be purple with white text</p>
      </div>
      
      <button className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded mr-4">
        Orange Button
      </button>
      
      <button className="bg-gray-800 hover:bg-gray-900 text-white font-bold py-2 px-4 rounded">
        Gray Button
      </button>
      
      <div className="mt-8 text-white">
        <p>If this page looks colorful and styled, Tailwind CSS is working correctly.</p>
        <p>If it looks plain or unstyled, there's a CSS compilation issue.</p>
      </div>
    </div>
  )
}
