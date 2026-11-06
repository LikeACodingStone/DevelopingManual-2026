package hardware.handbook.echo;

// @VintfStability: the interface may cross the system/vendor boundary, so it must be frozen
// per version and declared in a VINTF manifest.
@VintfStability
interface IEcho {
    String echo(in String text);
}
