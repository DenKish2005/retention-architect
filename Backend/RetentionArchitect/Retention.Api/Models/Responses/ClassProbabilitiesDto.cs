namespace Retention.Api.Models.Responses;

public class ClassProbabilitiesDto
{
    public double Stay { get; set; }
    public double VoluntaryChurn { get; set; }
    public double InvoluntaryChurn { get; set; }
}