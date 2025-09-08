// Quick test to verify Eye and EyeOff icons from lucide-react
import { Eye, EyeOff } from 'lucide-react';

console.log('Eye icon:', Eye);
console.log('EyeOff icon:', EyeOff);

// Test component
const TestComponent = () => {
    return (
        <div>
            <Eye />
            <EyeOff />
        </div>
    );
};

export default TestComponent;