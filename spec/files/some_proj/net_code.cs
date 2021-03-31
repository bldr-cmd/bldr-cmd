using System;

class SomeModule
{
    public SomeModule()
    {
        SomeOther.Nested.Place.Function()
    }

    ~SomeModule()
    {

    }
}

class SomeModuleVerySimilar: SomeModule
{

    public SomeModuleVerySimilar()
    {
        APlugableModule.CoolFunction(1,2,3)
    }

    ~SomeModuleVerySimilar()
    {

    }
}